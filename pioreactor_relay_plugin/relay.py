import json
       
from pioreactor.hardware import PWM_TO_PIN
from pioreactor.utils.pwm import PWM
from pioreactor.utils import clamp
from pioreactor.config import config
from pioreactor.background_jobs.base import BackgroundJob
from pioreactor.whoami import get_unit_name, get_latest_experiment_name

class Relay(BackgroundJob):

    published_settings = {
        "on": {"datatype": "boolean", "settable": True},
    }

    def __init__(self, hz, unit, experiment, start_on = True, **kwargs):
        super().__init__(job_name="relaym", unit=unit, experiment=experiment)
        self.hz = hz
        
        if start_on:
            self.duty_cycle = 100
            self.on = True
        else: 
            self.duty_cycle = 0
            self.on = False
            
        self.pwm_pin = PWM_TO_PIN[config.getint("PWM_reverse", "relay")]
        # looks at config.ini/configuration on UI to match 
        # changed PWM channel 2 to "relay" on leader
        # whatevers connected to channel 2 will turn on/off 

        self.pwm = PWM(self.pwm_pin, self.hz)
        self.pwm.lock()

    def set_on(self, value):
        if value:
            self.set_duty_cycle(100)
            self.on = True
        else:
            self.set_duty_cycle(0)
            self.on = False

    def set_duty_cycle(self, new_duty_cycle):
        self.duty_cycle = float(new_duty_cycle)
        self.pwm.change_duty_cycle(self.duty_cycle)

    def on_init_to_ready(self):
        self.pwm.start(self.duty_cycle)

    def on_ready_to_sleeping(self):
        self.set_on(False)

    def on_sleeping_to_ready(self):
        self.set_on(True)

    def on_disconnected(self):
        self.set_on(False)
        self.pwm.cleanup()
        
import click

@click.command(name="relay")
@click.option(
    "--hz",
    default=config.getfloat("relay", "hz"),
    show_default=True,
    type=click.FloatRange(1, 10_000, clamp=True),
)
@click.option(
    "--start-off",
    is_flag = True
)
def click_relay(hz, start_off):
    """
    Start the relay
    """
    job = Relay(
        hz=hz,
        unit=get_unit_name(),
        experiment=get_latest_experiment_name(),
        start_on = not start_off
    )
    job.block_until_disconnected()