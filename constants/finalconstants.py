ema_a_period = 14
ema_b_period = 18
signal_period = 12
cci_constant = 0.015
cci_upper_limit = 240
cci_lower_limit = 150
cci_period = 22
bollinger_band_sma_period = 20
stochastic_oscillator_period = 20
rsi_period = 20
rsi_upper_limit = 75
rsi_lower_limit = 25
bollinger_band_stdev_multiplier = 3.25


def get_cci_log_values():
    return "\nConstants:\nCCI Upper Limit: {}\nCCI Lower Limit: {}\nCCI Period: {}\nCCI Constant: {}\n" \
        .format(cci_upper_limit, -cci_lower_limit, cci_period, cci_constant)
