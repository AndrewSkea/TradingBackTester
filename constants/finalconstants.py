ema_a_period = 14
ema_b_period = 18
signal_period = 12

cci_constant = 0.015
cci_upper_limit = 160
cci_lower_limit = 130
cci_period = 15

stochastic_oscillator_period = 20

rsi_period = 18
rsi_upper_limit = 73
rsi_lower_limit = 21

bollinger_band_sma_period = 20
bollinger_band_stdev_multiplier = 2

adx_period = 22


def get_cci_log_values():
    return "\nConstants:\nCCI Upper Limit: {}\nCCI Lower Limit: {}\nCCI Period: {}\nCCI Constant: {}\n" \
        .format(cci_upper_limit, -cci_lower_limit, cci_period, cci_constant)
