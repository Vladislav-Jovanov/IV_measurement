#!/usr/bin/env python3

from submodules.Hub import MultipleApps

from GUIs.PS_AM.PS_AM import PowerSupply_AmMeter
from GUIs.VM_AM.VM_AM import VolMeter_AmMeter


#MultipleApps(app_list={'PS AM':PowerSupply_AmMeter, 'VM AM':VolMeter_AmMeter}).init_start()

MultipleApps(app_list={'PS AM':PowerSupply_AmMeter}).init_start()
