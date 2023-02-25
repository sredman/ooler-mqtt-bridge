#!/usr/bin/env python3

## Filename: ooler_ctrl.py
## Description: Interactive tool to issue BLE commands to control the Ooler bed cooler.

import asyncio
import argparse
from collections import namedtuple

from ooler import Ooler
import ooler.constants

Command = namedtuple("Command", ["read_action", "write_action"])

commands = {
    "power": Command(Ooler.powered_on, Ooler.set_power_state),
    "target_temp": Command(Ooler.get_desired_temperature_f, Ooler.set_desired_temperature_f),
    #"actualTemp": Command("actualTemp", ooler.constants.ACTUAL_TEMP),
}

async def main():
    parser = argparse.ArgumentParser(
        prog="OolerCtrl",
        description="Control the Ooler bed cooler using BLE"
    )
    parser.add_argument("--MAC", required=True,
        help="MAC address of the Ooler to control, like AA:BB:CC:DD:EE:FF")
    subparsers = parser.add_subparsers(title="Commands", description="Command to issue", required=True)

    power_parser = subparsers.add_parser("power",
        help="Ooler power state")
    power_parser.add_argument("--state", choices=["auto", "off"], required=False,
        help="Desired power state")
    power_parser.set_defaults(func=handle_power)

    target_temp_parser = subparsers.add_parser("target_temp",
        help="Device target temperature (F)")
    target_temp_parser.add_argument("--temp", type=int,
        help="Desired target temperature")
    target_temp_parser.set_defaults(func=handle_target_temp)

    args = parser.parse_args()

    ooler = Ooler(address=args.MAC)

    result = await args.func(ooler, args)

    print(result)

async def handle_power(ooler: Ooler, args):
    if args.state is not None:
        return await ooler.set_power_state(True if args.state == "auto" else False)

    return await ooler.powered_on()

async def handle_target_temp(ooler: Ooler, args):
    if args.temp is not None:
        return await ooler.set_desired_temperature_f(args.temp)

    return await ooler.get_desired_temperature_f()

if __name__ == "__main__":
    asyncio.run(main())