import os
import yaml
try:
    import notify2
    notify_module = True
except ModuleNotFoundError as e:
    print(f"ERROR: During improt of notify2 module",
          " this error appeared: {e}. Notifications are disabled.")
    notify_module = False


def send_notification(title, message):
    if notify_module:
        notify2.init('Teleserver')
        notice = notify2.Notification(title, message)
        notice.show()


def check_if_condition_true(real_value, operator, test_value):
    try:
        real = float(real_value)
        test = float(test_value)
    except ValueError:
        raise(f'ERROR: Either value from sensor {real_value} or value '
              'from configuration {test_value} is not proper.')
        return False
    try:
        result = eval(f'{real}{operator}{test}')
        return result
    except SyntaxError:
        raise(f'ERROR: Invalid operator {operator}!')
        return False


def check_notification_conditions(data, conditions):
    result = True
    for key in conditions.keys():
        if key in data.keys():
            result = result and check_if_condition_true(data[key],
                                                        conditions[key]['operator'],
                                                        conditions[key]['value'])
        else:
            return False
    else:
        return result


def check_data_and_execute_notifications(data):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    with open(f'{dir_path}/files/notifications_config.yml', 'r') as config_file:
        notifications = yaml.safe_load(config_file)
    for notification in notifications:
        if check_notification_conditions(data, notification['conditions']):
            send_notification(notification['title'], notification['message'])
