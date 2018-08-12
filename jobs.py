from string import Template
import textwrap


def get_template():
    return textwrap.dedent(
        """
    import time
    import math
    import json

    time.sleep($delay)

    x = [x*0.01 for x in range(1, 314)]
    y = [math.$transform(xi * $modifier) for xi in x]

    payload = {'x': x, 'y': y}

    print(json.dumps(payload))
    """
    )


def get_job_data(modifier, transform, delay=10):
    template = Template(get_template())
    templated_string = template.substitute(
        delay=delay, transform=transform, modifier=modifier
    )

    return {"code": templated_string}
