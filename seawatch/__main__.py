"""Entry point and main logic of the Sea Watch script."""
import datetime
import os
import sys
import time
import yaml

from termcolor import colored
from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer


__all__ = ('main',)


services = dict()


def cprint(str_, color=None, timestamped=True):
    """Print in color and with a timestamp if needed."""
    timestamp = datetime.datetime.now().strftime('%H:%M:%S')
    if timestamped:
        str_ = '%s: %s' % (timestamp, str_)
    print(colored(str_, color))


def get_services_from_compose_data(compose_data):
    """Extract services from the data of a compose file as a dict."""
    services_dict = dict()

    for k, v in compose_data['services'].items():
        # Handle services built from local Dockerfiles.
        if 'build' in v:
            if isinstance(v['build']) is not str:
                raise ValueError("Nested build options are not supported " +
                                 "at the moment")

            services_dict[k] = v['build']
        # Handle services built from external images.
        if 'image' in v:
            services_dict[k] = v['image']

    return services_dict


class CodeChangeHandler(PatternMatchingEventHandler):
    """Handler class to rebuild and update services when their code changes."""

    def __init__(self, patterns):
        super(CodeChangeHandler, self).__init__(patterns=patterns)

    def on_modified(self, event):
        """Execute for every file change event matching the patterns."""
        affected_services = [s for s in services
                             if services[s] in event.src_path]
        if len(affected_services) == 1:
            affected_service = affected_services[0]
            cprint("Changes in service '%s' detected." % affected_service,
                   'yellow')
            cprint("The following running instances are affected:")
            terminal_output = os.popen('docker-compose ps').read()
            service_names = [l.split()[0] for l in
                             terminal_output.split('\n')[2:-1]]
            affected_instances = []
            for sn in service_names:
                if affected_service in sn:
                    affected_instances.append(sn)
            for sn in affected_instances:
                cprint("\t%s" % sn, 'blue', timestamped=False)

            # Restart service through Docker Compose.
            os.popen('docker-compose up -d --no-deps --build %s'
                     % affected_service).read()


def main():
    """Entrypoint to the ``seawatch`` umbrella command."""
    global services

    args = sys.argv[1:]
    if len(args) < 2:
        cprint("Usage: python run.py <path to docker-compose.yml> " +
               "[observed file extensions]",
               'red', timestamped=False)
        sys.exit(1)

    yml_path = args[0]
    if not yml_path.endswith('docker-compose.yml'):
        cprint("Please point to 'docker-compose.yml' file.",
               'red', timestamped=False)
        sys.exit(1)

    observed_file_extensions = args[1:]

    # Read docker-compose.yml.
    with open(yml_path, 'r') as stream:
        try:
            compose_data = yaml.load(stream)
        except yaml.YAMLError as exc:
            cprint(exc, 'red')
            sys.exit(1)

    services = get_services_from_compose_data(compose_data)

    base_dir = os.path.dirname(os.path.realpath(yml_path))
    os.chdir(base_dir)
    cprint("Sea Watch is now observing %s files for '%s'."
           % (observed_file_extensions, base_dir), 'green')

    # Start observer.
    patterns = [r'*.%s' % extension for extension in observed_file_extensions]
    event_handler = CodeChangeHandler(patterns=patterns)
    observer = Observer()
    observer.schedule(event_handler, base_dir, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(100)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == '__main__':
    main()
