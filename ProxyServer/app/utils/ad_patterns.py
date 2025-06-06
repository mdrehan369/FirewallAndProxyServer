import re

ad_patterns = [
    re.compile(r".*doubleclick\.net.*"),
    re.compile(r".*googleadservices\.com.*"),
    re.compile(r".*googlesyndication\.com.*"),
    re.compile(r".*adsafeprotected\.com.*"),
    re.compile(r".*adnxs\.com.*"),
    re.compile(r".*moatads\.com.*"),
    re.compile(r".*criteo\.com.*"),
    re.compile(r".*adform\.net.*"),
    re.compile(r".*scorecardresearch\.com.*"),
    re.compile(r".*serving-sys\.com.*"),
    re.compile(r".*contextweb\.com.*"),
    re.compile(r".*zedo\.com.*"),
    re.compile(r".*openx\.net.*"),
    re.compile(r".*pubmatic\.com.*"),
    re.compile(r".*yieldmanager\.com.*"),
    re.compile(r".*casalemedia\.com.*"),
    re.compile(r".*tribalfusion\.com.*"),
    re.compile(r".*media\.net.*"),
    re.compile(r".*tapad\.com.*"),
    re.compile(r".*bidswitch\.net.*"),
    re.compile(r".*advertising\.com.*"),
    re.compile(r".*outbrain\.com.*"),
    re.compile(r".*taboola\.com.*"),
    re.compile(r".*rubiconproject\.com.*"),
    re.compile(r".*lijit\.com.*"),
    re.compile(r".*revcontent\.com.*"),
    re.compile(r".*spotxchange\.com.*"),
    re.compile(r".*360yield\.com.*"),
    re.compile(r".*bluekai\.com.*"),
    re.compile(r".*mathtag\.com.*"),
    re.compile(r".*ml314\.com.*"),
    re.compile(r".*simpli\.fi.*"),
    re.compile(r".*rfihub\.com.*"),
    re.compile(r".*yieldmo\.com.*"),
    re.compile(r".*onetag-sys\.com.*"),
    re.compile(r".*g\.doubleclick\.net.*"),
    re.compile(r".*youtube\.com/api/stats/ads.*"),
    re.compile(r".*youtube\.com/pagead/.*"),
    re.compile(r".*youtube\.com/get_midroll_info.*"),
    re.compile(r".*googleads\.g\.doubleclick\.net/pagead/id.*"),
    re.compile(r".*doubleclick\.net/pagead/.*"),
    re.compile(r".*youtube\.com/ptracking.*"),
    re.compile(r".*youtube\.com/videoplayback.*&(oad|adformat)=.*"),
    re.compile(r".*youtube\.com/ad_break.*"),
    re.compile(r".*youtube\.com/ptracking.*"),
    re.compile(r".*youtube\.com/yva_video.*"),
    re.compile(r".*steadfastsystem\.com/.*"),
    re.compile(r".*adtrafficquality\.google/.*"),
    re.compile(r".*bannersnack\.com/.*"),
    re.compile(r".*adsafeprotected\.com/.*"),
    re.compile(r".*videoplayback.*(adformat|oad)=.*")
]

