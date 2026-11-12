"""Default list of tickers to scan.

These are US-listed names that have historically moved a lot and still trade
enough volume to buy and sell easily. The list is only a starting point: the
scanner measures how volatile each one is *right now* and ranks them.
Edit it freely, or pass your own with --tickers / --file.
"""

DEFAULT_UNIVERSE = sorted(set("""
TSLA NVDA AMD SMCI PLTR COIN MSTR HOOD RIVN LCID NIO XPEV LI
MARA RIOT CLSK HUT CIFR WULF IREN CORZ
GME AMC SOFI AFRM UPST XYZ PYPL SHOP ROKU SNAP PINS RBLX U DKNG
NET CRWD SNOW DDOG MDB ZS OKTA TWLO PATH AI SOUN BBAI
IONQ RGTI QBTS QUBT ARQQ
ACHR JOBY LUNR RKLB ASTS SPCE
ENPH FSLR RUN SEDG PLUG FCEL BE CHPT QS
MRNA BNTX NVAX CRSP BEAM NTLA EDIT VKTX
CVNA W CHWY ETSY CELH ELF
CCL NCLH RCL AAL UAL
TQQQ SQQQ SOXL SOXS TNA LABU UVXY
ARM AVGO MU INTC WOLF ON
APP DUOL TTD
OKLO SMR NNE CEG VST
CAVA HIMS ONON
""".split()))

# Leveraged / inverse ETFs decay over time by design. They are volatile but are
# a poor fit for buy-and-hold dollar-cost averaging, so they are excluded unless
# you ask for them with --include-leveraged.
LEVERAGED_ETFS = {"TQQQ", "SQQQ", "SOXL", "SOXS", "TNA", "LABU", "UVXY"}
