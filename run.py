import datetime
import os
import sys
from termcolor import colored
import time
import yaml

from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer


def cprint(str_, color=None, timestamped=True):
    """Print in color and with a timestamp if needed."""
    timestamp = datetime.datetime.now().strftime('%H:%M:%S')
    if timestamped:
        str_ = '%s: %s' % (timestamp, str_)
    print(colored(str_, color))


class CodeChangeHandler(PatternMatchingEventHandler):
    """Handler class to rebuild and update services when their code changes."""

    patterns = ['*.py']

    def on_modified(self, event):
        """Execute for every file change event."""
        if event.src_path.endswith('.py'):
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


if __name__ == "__main__":
    global services

    args = sys.argv[1:]

    if len(args) != 1:
        sys.exit(1)

    yml_path = args[0]
    if not yml_path.endswith('docker-compose.yml'):
        sys.exit(1)

    # Read docker-compose.yml.
    with open(yml_path, 'r') as stream:
        try:
            compose_data = yaml.load(stream)
        except yaml.YAMLError as exc:
            cprint(exc, 'red')
            sys.exit(1)

    services = {k: v['build'] for k, v in compose_data['services'].items()}

    base_dir = os.path.dirname(os.path.realpath(yml_path))
    os.chdir(base_dir)
    cprint("Sea Watch is now observing '%s'." % base_dir, 'green')

    # Start observer.
    event_handler = CodeChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, base_dir, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(100)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
