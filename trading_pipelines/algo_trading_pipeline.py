from quantopian.algorithm import attach_pipeline.pipeline_output
from quantopian.pipeline import Pipeline
from quantopian.pipeline.data.builtin import USEquityPricing
from quantopian.pipeline.factors import AverageDollarVolume.SimpleMovingAverage
from quantopian.pipeline.filters.morningstar import Q1500US
from quantopian.pipeline.data import morningstar

def initialize(context):
    schedule_function(my_rebalance,data_rules.week_start(),time_rules.market_open(hours=1))
    my_pipe = make_pipeline()
    attach_pipeline(my_pipe,"my_pipeline")

def my_rebalance(context,data):
    for security in context.portfolio.positions:
        if security not in context.longs and security not in context.shorts and data.can_trade(security):
            order_target_percent(security,0)
    
    for security in context.longs:
        if data.can_trade(security):
            order_target_percent(security,context.long_weight)

    for security in context.shorts:
        if data.can_trade(security):
            order_target_percent(security,context.short_weight)

def my_compute_weights(context):
    if (context.longs) == 0:
        long_weight = 0
    else:
        long_weight = 0.5 / len(context.longs)
    if (context.shorts) == 0:
        short_weight = 0
    else:
        short_weight = -0.5 /len(context.shorts)

    return (long_weight,short_weight)

def before_trading_start(context,data):
    context.output = pipeline_output('my_pipeline')

    # LONG
    context.longs = context.output[context.output['longs'].index.tolist()]
    # SHORT
    context.shorts = context.output[context.output['shorts'].index.tolist()]

    context.long_weight, context.short_weight = my_compute_weights(context)

def make_pipeline():
    # Universe Q1500US
    base_universe = Q1500US()

    # Energy Sector
    sector = morningstar.assest_classification.morningstar_sector_code.latest
    energy_sector = sector.eq(309)

    # Make Mask of 1500US and Energy
    base_energy = base_universe & energy_sector

    # Dollar Vollume (30 Days) Grab the Info
    dollar_volume = AverageDollarVolume(window_length=30)

    # Grab top 5% of dollar volume
    high_dollar_volume = dollar_volume.percentile_between(95,100)

    # Combine the filters
    top_five_base_energy = base_energy & high_dollar_volume

    # 10 Days Mean Close
    mean_10 = SimpleMovingAverage(inputs=[USEquityPricing.close],window_length=10,mask=top_five_base_energy)
    
    # 30 Days Mean Close
    mean_30 = SimpleMovingAverage(inputs=[USEquityPricing.close],window_length=30,mask=top_five_base_energy)

    # Percent Difference
    percent_difference = (mean_10 - mean_30)/mean_30

    # List of Shorts
    shorts = percent_difference < 0 

    # List of Longs
    longs = percent_difference > 0

    # Final Mask/Filter for anything in shorts or longs
    securities_to_trade = (shorts | longs)

    # Return Pipeline
    return Pipeline(columns={
        'longs':longs,
        'shorts':shorts,
        'perc_diff':percent_difference
    },screen=securities_to_trade)

