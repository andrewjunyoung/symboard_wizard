from symboard.states import load_yaml
from tabulate import tabulate


def format_outputs(state):
    return ''.join(state.action_to_output_map.values())


def main() -> None:
    states = load_yaml()

    headers = ['Name', 'Terminator', 'Outputs']
    data = [
        [state.name, state.terminator, format_outputs(state)]
        for state in states.values()
    ]

    print(tabulate(data, headers=headers, tablefmt='orgtbl'))


if __name__ == '__main__':
    main()
