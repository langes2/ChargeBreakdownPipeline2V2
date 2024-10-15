@echo off
python "C:\Users\Public\Documents\ChargeBreakdownPipeline\CBfragments\CBfrags_firstfourclean.py" > "C:\Users\Public\Documents\ChargeBreakdownPipeline\CBfragments\Fraglogs\CBfirstfourclean1log.log" 2>&1
python "C:\Users\Public\Documents\ChargeBreakdownPipeline\CBfragments\CBfrags_firstfourclean2.py" > "C:\Users\Public\Documents\ChargeBreakdownPipeline\CBfragments\Fraglogs\CBfirstfourclean2log.log" 2>&1
python "C:\Users\Public\Documents\ChargeBreakdownPipeline\CBfragments\CBfrags_firstfourclean3.py" > "C:\Users\Public\Documents\ChargeBreakdownPipeline\CBfragments\Fraglogs\CBfirstfourclean3log.log" 2>&1
python "C:\Users\Public\Documents\ChargeBreakdownPipeline\CBfragments\CBfrags_fifthclean.py" > "C:\Users\Public\Documents\ChargeBreakdownPipeline\CBfragments\Fraglogs\CBfifthclean1log.log" 2>&1
python "C:\Users\Public\Documents\ChargeBreakdownPipeline\CBfragments\CBfrags_fifthclean2.py" > "C:\Users\Public\Documents\ChargeBreakdownPipeline\CBfragments\Fraglogs\CBfifthclean2log.log" 2>&1
python "C:\Users\Public\Documents\ChargeBreakdownPipeline\CBfragments\CBfrags_fifthclean3.py" > "C:\Users\Public\Documents\ChargeBreakdownPipeline\CBfragments\Fraglogs\CBfifthclean3log.log" 2>&1
python "C:\Users\Public\Documents\ChargeBreakdownPipeline\CBfragments\CBcombinefrags.py" > "C:\Users\Public\Documents\ChargeBreakdownPipeline\CBfragments\Fraglogs\combinelogs.log" 2>&1
python "C:\Users\Public\Documents\ChargeBreakdownPipeline\CBfragments\writeoverdupes.py" > "C:\Users\Public\Documents\ChargeBreakdownPipeline\CBfragments\Fraglogs\dupeslog.log" 2>&1
python "C:\Users\Public\Documents\ChargeBreakdownPipeline\CBfragments\sqlconnect.py" > "C:\Users\Public\Documents\ChargeBreakdownPipeline\CBfragments\Fraglogs\sqllog.log" 2>&1