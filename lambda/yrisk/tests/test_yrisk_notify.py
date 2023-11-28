import logging
import unittest
import copy

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import yrisk_functions

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class YriskNotifyTestCase(unittest.TestCase):

    json_data = {
    "start": "2021-08-01 00:00:00",
    "end": "2021-08-31 23:59:59",
    "vehicles": [
        {
            "vin": "DEV-7F7ATR312MER00159",
            "location": {
                "name": "Arcimoto Rental Facility [Eugene]",
                "city": "Eugene",
                "state": "Oregon"
            },
            "coverage": "rental",
            "model": "FUV",
            "telemetry": {
                "odometer": {
                    "start": {
                        "point": 5.30029463,
                        "time": "2021-08-23T20:23:00Z"
                    },
                    "end": {
                        "point": 163.87417383000002,
                        "time": "2021-08-30T22:42:00Z"
                    }
                }
            }
        },
        {
            "vin": "DEV-7F7ATR313LER00010",
            "location": {
                "name": "Arcimoto World Headquarters",
                "city": "Eugene",
                "state": "Oregon"
            },
            "coverage": "internal",
            "model": "FUV",
            "telemetry": {
                "odometer": "unknown"
            }
        },
        {
            "vin": "DEV-7F7ATR313LER00038",
            "location": {
                "name": "Arcimoto World Headquarters",
                "city": "Eugene",
                "state": "Oregon"
            },
            "coverage": "internal",
            "model": "FUV",
            "telemetry": {
                "odometer": "unknown"
            }
        },
        {
            "vin": "DEV-7F7ATR313LER00086",
            "location": {
                "name": "Arcimoto World Headquarters",
                "city": "Eugene",
                "state": "Oregon"
            },
            "coverage": "internal",
            "model": "FUV",
            "telemetry": {
                "odometer": "unknown"
            }
        },
        {
            "vin": "DEV-7F7ATR313MER00073",
            "location": {
                "name": "Arcimoto Rental Facility [Eugene]",
                "city": "Eugene",
                "state": "Oregon"
            },
            "coverage": "rental",
            "model": "FUV",
            "telemetry": {
                "odometer": "unknown"
            }
        },
        {
            "vin": "DEV-7F7ATR313MER00087",
            "location": {
                "name": "Arcimoto Rental Facility [Eugene]",
                "city": "Eugene",
                "state": "Oregon"
            },
            "coverage": "rental",
            "model": "FUV",
            "telemetry": {
                "odometer": "unknown"
            }
        },
        {
            "vin": "DEV-7F7ATR313MER00090",
            "location": {
                "name": "Arcimoto Rental Facility [Eugene]",
                "city": "Eugene",
                "state": "Oregon"
            },
            "coverage": "rental",
            "model": "FUV",
            "telemetry": {
                "odometer": {
                    "start": {
                        "point": 2206.78667908,
                        "time": "2021-08-22T00:11:00Z"
                    },
                    "end": {
                        "point": 2488.92639534,
                        "time": "2021-08-31T21:16:00Z"
                    }
                }
            }
        },
        {
            "vin": "DEV-7F7ATR313MER00137",
            "location": {
                "name": "Arcimoto World Headquarters",
                "city": "Eugene",
                "state": "Oregon"
            },
            "coverage": "pilot",
            "model": "FUV",
            "telemetry": {
                "odometer": {
                    "start": {
                        "point": 5.30029463,
                        "time": "2021-08-23T19:38:00Z"
                    },
                    "end": {
                        "point": 5.3437906,
                        "time": "2021-08-31T20:09:00Z"
                    }
                }
            }
        },
        {
            "vin": "DEV-7F7ATR313MER00154",
            "location": {
                "name": "Arcimoto Rental Facility [Eugene]",
                "city": "Eugene",
                "state": "Oregon"
            },
            "coverage": "rental",
            "model": "FUV",
            "telemetry": {
                "odometer": {
                    "start": {
                        "point": 6.71702051,
                        "time": "2021-08-23T20:30:00Z"
                    },
                    "end": {
                        "point": 61.36659996,
                        "time": "2021-08-30T22:45:00Z"
                    }
                }
            }
        },
        {
            "vin": "DEV-7F7ATR314KER00015",
            "location": {
                "name": "Arcimoto World Headquarters",
                "city": "Eugene",
                "state": "Oregon"
            },
            "coverage": "pilot",
            "model": "FUV",
            "telemetry": {
                "odometer": "unknown"
            }
        },
        {
            "vin": "DEV-7F7ATR314KER00032",
            "location": {
                "name": "Arcimoto World Headquarters",
                "city": "Eugene",
                "state": "Oregon"
            },
            "coverage": "internal",
            "model": "FUV",
            "telemetry": {
                "odometer": {
                    "start": {
                        "point": 2835.65141334,
                        "time": "2021-08-22T20:48:00Z"
                    },
                    "end": {
                        "point": 2915.56593765,
                        "time": "2021-08-31T21:39:00Z"
                    }
                }
            }
        },
        {
            "vin": "DEV-7F7ATR314LER00047",
            "location": {
                "name": "Arcimoto World Headquarters",
                "city": "Eugene",
                "state": "Oregon"
            },
            "coverage": "pilot",
            "model": "FUV",
            "telemetry": {
                "odometer": {
                    "start": {
                        "point": 1382.82387824,
                        "time": "2021-08-24T19:27:00Z"
                    },
                    "end": {
                        "point": 1399.48904846,
                        "time": "2021-08-30T03:51:00Z"
                    }
                }
            }
        },
        {
            "vin": "DEV-7F7ATR314LER00081",
            "location": {
                "name": "Arcimoto World Headquarters",
                "city": "Eugene",
                "state": "Oregon"
            },
            "coverage": "internal",
            "model": "FUV",
            "telemetry": {
                "odometer": {
                    "start": {
                        "point": 3454.99674388,
                        "time": "2021-08-23T11:36:00Z"
                    },
                    "end": {
                        "point": 3510.30497659,
                        "time": "2021-08-30T19:14:00Z"
                    }
                }
            }
        },
        {
            "vin": "DEV-7F7ATR314MER00082",
            "location": {
                "name": "Arcimoto World Headquarters",
                "city": "Eugene",
                "state": "Oregon"
            },
            "coverage": "pilot",
            "model": "FUV",
            "telemetry": {
                "odometer": "unknown"
            }
        },
        {
            "vin": "DEV-7F7ATR314MER00129",
            "location": {
                "name": "Arcimoto Rental Facility [San Diego]",
                "city": "San Diego",
                "state": "California"
            },
            "coverage": "rental",
            "model": "FUV",
            "telemetry": {
                "odometer": {
                    "start": {
                        "point": 369.12544255,
                        "time": "2021-08-22T18:20:00Z"
                    },
                    "end": {
                        "point": 451.33903956,
                        "time": "2021-08-31T20:51:00Z"
                    }
                }
            }
        },
        {
            "vin": "DEV-7F7ATR314MER00132",
            "location": {
                "name": "Arcimoto Rental Facility [San Diego]",
                "city": "San Diego",
                "state": "California"
            },
            "coverage": "rental",
            "model": "FUV",
            "telemetry": {
                "odometer": {
                    "start": {
                        "point": 104.52081591000001,
                        "time": "2021-08-23T15:56:00Z"
                    },
                    "end": {
                        "point": 178.71251331000002,
                        "time": "2021-08-31T22:26:00Z"
                    }
                }
            }
        },
        {
            "vin": "DEV-7F7ATR314MER00163",
            "location": {
                "name": "Arcimoto World Headquarters",
                "city": "Eugene",
                "state": "Oregon"
            },
            "coverage": "internal",
            "model": "FUV",
            "telemetry": {
                "odometer": {
                    "start": {
                        "point": 95.20025091000001,
                        "time": "2021-08-22T13:14:00Z"
                    },
                    "end": {
                        "point": 483.84917027999995,
                        "time": "2021-08-31T16:47:00Z"
                    }
                }
            }
        },
        {
            "vin": "DEV-7F7ATR315LER00011",
            "location": {
                "name": "Arcimoto World Headquarters",
                "city": "Eugene",
                "state": "Oregon"
            },
            "coverage": "internal",
            "model": "FUV",
            "telemetry": {
                "odometer": "unknown"
            }
        },
        {
            "vin": "DEV-7F7ATR315LER00042",
            "location": {
                "name": "Arcimoto World Headquarters",
                "city": "Eugene",
                "state": "Oregon"
            },
            "coverage": "internal",
            "model": "FUV",
            "telemetry": {
                "odometer": {
                    "start": {
                        "point": 1143.09894644,
                        "time": "2021-08-23T16:04:00Z"
                    },
                    "end": {
                        "point": 1208.24348208,
                        "time": "2021-08-29T12:48:00Z"
                    }
                }
            }
        },
        {
            "vin": "DEV-7F7ATR315LER00087",
            "location": {
                "name": "Arcimoto World Headquarters",
                "city": "Eugene",
                "state": "Oregon"
            },
            "coverage": "internal",
            "model": "FUV",
            "telemetry": {
                "odometer": {
                    "start": {
                        "point": 3028.50633061,
                        "time": "2021-08-22T01:14:00Z"
                    },
                    "end": {
                        "point": 3138.0540379100003,
                        "time": "2021-08-31T04:59:00Z"
                    }
                }
            }
        },
        {
            "vin": "DEV-7F7ATR315MER00074",
            "location": {
                "name": "Arcimoto Rental Facility [Eugene]",
                "city": "Eugene",
                "state": "Oregon"
            },
            "coverage": "rental",
            "model": "FUV",
            "telemetry": {
                "odometer": "unknown"
            }
        },
        {
            "vin": "DEV-7F7ATR315MER00091",
            "location": {
                "name": "Arcimoto Rental Facility [Eugene]",
                "city": "Eugene",
                "state": "Oregon"
            },
            "coverage": "rental",
            "model": "FUV",
            "telemetry": {
                "odometer": "unknown"
            }
        },
        {
            "vin": "DEV-7F7ATR315MER00138",
            "location": {
                "name": "Arcimoto World Headquarters",
                "city": "Eugene",
                "state": "Oregon"
            },
            "coverage": "pilot",
            "model": "FUV",
            "telemetry": {
                "odometer": {
                    "start": {
                        "point": 5.39350028,
                        "time": "2021-08-27T16:23:00Z"
                    },
                    "end": {
                        "point": 5.840887400000001,
                        "time": "2021-08-31T22:20:00Z"
                    }
                }
            }
        },
        {
            "vin": "DEV-7F7ATR315MER00155",
            "location": {
                "name": "Arcimoto Rental Facility [Eugene]",
                "city": "Eugene",
                "state": "Oregon"
            },
            "coverage": "rental",
            "model": "FUV",
            "telemetry": {
                "odometer": {
                    "start": {
                        "point": 5.44320996,
                        "time": "2021-08-23T20:23:00Z"
                    },
                    "end": {
                        "point": 75.93774991,
                        "time": "2021-08-30T22:55:00Z"
                    }
                }
            }
        },
        {
            "vin": "DEV-7F7ATR316LER00082",
            "location": {
                "name": "Arcimoto World Headquarters",
                "city": "Eugene",
                "state": "Oregon"
            },
            "coverage": "internal",
            "model": "FUV",
            "telemetry": {
                "odometer": {
                    "start": {
                        "point": 1745.431139,
                        "time": "2021-08-23T13:40:00Z"
                    },
                    "end": {
                        "point": 1750.19705457,
                        "time": "2021-08-30T21:03:00Z"
                    }
                }
            }
        },
        {
            "vin": "DEV-7F7ATR316MER00097",
            "location": {
                "name": "Arcimoto Rental Facility [Orlando]",
                "city": "Orlando",
                "state": "Florida"
            },
            "coverage": "rental",
            "model": "FUV",
            "telemetry": {
                "odometer": "unknown"
            }
        },
        {
            "vin": "DEV-7F7ATR316MER00102",
            "location": {
                "name": "Arcimoto World Headquarters",
                "city": "Eugene",
                "state": "Oregon"
            },
            "coverage": "internal",
            "model": "FUV",
            "telemetry": {
                "odometer": "unknown"
            }
        },
        {
            "vin": "DEV-7F7ATR316MER00133",
            "location": {
                "name": "Arcimoto Rental Facility [San Diego]",
                "city": "San Diego",
                "state": "California"
            },
            "coverage": "rental",
            "model": "FUV",
            "telemetry": {
                "odometer": {
                    "start": {
                        "point": 262.57274347,
                        "time": "2021-08-22T19:33:00Z"
                    },
                    "end": {
                        "point": 451.04699519,
                        "time": "2021-08-31T01:38:00Z"
                    }
                }
            }
        },
        {
            "vin": "DEV-7F7ATR316MER00164",
            "location": {
                "name": "Arcimoto World Headquarters",
                "city": "Eugene",
                "state": "Oregon"
            },
            "coverage": "pilot",
            "model": "FUV",
            "telemetry": {
                "odometer": {
                    "start": {
                        "point": 92.18660156000001,
                        "time": "2021-08-22T16:17:00Z"
                    },
                    "end": {
                        "point": 104.96820303000001,
                        "time": "2021-08-30T19:23:00Z"
                    }
                }
            }
        },
        {
            "vin": "DEV-7F7ATR317LER00088",
            "location": {
                "name": "Arcimoto World Headquarters",
                "city": "Eugene",
                "state": "Oregon"
            },
            "coverage": "internal",
            "model": "FUV",
            "telemetry": {
                "odometer": {
                    "start": {
                        "point": 2416.62366578,
                        "time": "2021-08-22T21:26:00Z"
                    },
                    "end": {
                        "point": 2524.1084213599997,
                        "time": "2021-08-31T19:07:00Z"
                    }
                }
            }
        },
        {
            "vin": "DEV-7F7ATR317MER00027",
            "location": {
                "name": "Arcimoto Rental Facility [San Diego]",
                "city": "San Diego",
                "state": "California"
            },
            "coverage": "rental",
            "model": "FUV",
            "telemetry": {
                "odometer": "unknown"
            }
        },
        {
            "vin": "DEV-7F7ATR317MER00030",
            "location": {
                "name": "Arcimoto Rental Facility [San Diego]",
                "city": "San Diego",
                "state": "California"
            },
            "coverage": "rental",
            "model": "FUV",
            "telemetry": {
                "odometer": "unknown"
            }
        },
        {
            "vin": "DEV-7F7ATR317MER00075",
            "location": {
                "name": "Arcimoto Rental Facility [Eugene]",
                "city": "Eugene",
                "state": "Oregon"
            },
            "coverage": "rental",
            "model": "FUV",
            "telemetry": {
                "odometer": "unknown"
            }
        },
        {
            "vin": "DEV-7F7ATR317MER00089",
            "location": {
                "name": "Arcimoto Rental Facility [Eugene]",
                "city": "Eugene",
                "state": "Oregon"
            },
            "coverage": "rental",
            "model": "FUV",
            "telemetry": {
                "odometer": {
                    "start": {
                        "point": 1696.5975921099998,
                        "time": "2021-08-22T00:03:00Z"
                    },
                    "end": {
                        "point": 2022.1276453,
                        "time": "2021-08-31T23:59:00Z"
                    }
                }
            }
        },
        {
            "vin": "DEV-7F7ATR317MER00092",
            "location": {
                "name": "Arcimoto Rental Facility [Eugene]",
                "city": "Eugene",
                "state": "Oregon"
            },
            "coverage": "rental",
            "model": "FUV",
            "telemetry": {
                "odometer": {
                    "start": {
                        "point": 2415.75374638,
                        "time": "2021-08-22T15:40:00Z"
                    },
                    "end": {
                        "point": 2721.26322595,
                        "time": "2021-08-31T20:17:00Z"
                    }
                }
            }
        },
        {
            "vin": "DEV-7F7ATR317MER00139",
            "location": {
                "name": "Arcimoto World Headquarters",
                "city": "Eugene",
                "state": "Oregon"
            },
            "coverage": "pilot",
            "model": "FUV",
            "telemetry": {
                "odometer": {
                    "start": {
                        "point": 5.983802730000001,
                        "time": "2021-08-23T21:21:00Z"
                    },
                    "end": {
                        "point": 6.449830980000001,
                        "time": "2021-08-31T22:22:00Z"
                    }
                }
            }
        },
        {
            "vin": "DEV-7F7ATR317MER00156",
            "location": {
                "name": "Arcimoto Rental Facility [Eugene]",
                "city": "Eugene",
                "state": "Oregon"
            },
            "coverage": "rental",
            "model": "FUV",
            "telemetry": {
                "odometer": "unknown"
            }
        },
        {
            "vin": "DEV-7F7ATR318KER00003",
            "location": {
                "name": "Arcimoto World Headquarters",
                "city": "Eugene",
                "state": "Oregon"
            },
            "coverage": "internal",
            "model": "FUV",
            "telemetry": {
                "odometer": "unknown"
            }
        },
        {
            "vin": "DEV-7F7ATR318LER00052",
            "location": {
                "name": "Arcimoto World Headquarters",
                "city": "Eugene",
                "state": "Oregon"
            },
            "coverage": "pilot",
            "model": "FUV",
            "telemetry": {
                "odometer": {
                    "start": {
                        "point": 435.63699439000004,
                        "time": "2021-08-23T03:16:00Z"
                    },
                    "end": {
                        "point": 509.69199017,
                        "time": "2021-08-31T19:10:00Z"
                    }
                }
            }
        },
        {
            "vin": "DEV-7F7ATR318LER00083",
            "location": {
                "name": "Arcimoto World Headquarters",
                "city": "Eugene",
                "state": "Oregon"
            },
            "coverage": "internal",
            "model": "FUV",
            "telemetry": {
                "odometer": "unknown"
            }
        },
        {
            "vin": "DEV-7F7ATR318MER00084",
            "location": {
                "name": "Arcimoto World Headquarters",
                "city": "Eugene",
                "state": "Oregon"
            },
            "coverage": "internal",
            "model": "FUV",
            "telemetry": {
                "odometer": "unknown"
            }
        },
        {
            "vin": "DEV-7F7ATR318MER00098",
            "location": {
                "name": "Arcimoto Rental Facility [Orlando]",
                "city": "Orlando",
                "state": "Florida"
            },
            "coverage": "rental",
            "model": "FUV",
            "telemetry": {
                "odometer": "unknown"
            }
        },
        {
            "vin": "DEV-7F7ATR318MER00134",
            "location": {
                "name": "Arcimoto Rental Facility [Eugene]",
                "city": "Eugene",
                "state": "Oregon"
            },
            "coverage": "rental",
            "model": "FUV",
            "telemetry": {
                "odometer": {
                    "start": {
                        "point": 5.4680648000000005,
                        "time": "2021-08-23T19:30:00Z"
                    },
                    "end": {
                        "point": 11.9303232,
                        "time": "2021-08-30T23:15:00Z"
                    }
                }
            }
        },
        {
            "vin": "DEV-7F7ATR319KER00009",
            "location": {
                "name": "Arcimoto World Headquarters",
                "city": "Eugene",
                "state": "Oregon"
            },
            "coverage": "internal",
            "model": "FUV",
            "telemetry": {
                "odometer": {
                    "start": {
                        "point": 1084.42909662,
                        "time": "2021-08-24T21:52:00Z"
                    },
                    "end": {
                        "point": 1195.71664272,
                        "time": "2021-08-31T21:54:00Z"
                    }
                }
            }
        },
        {
            "vin": "DEV-7F7ATR319LER00044",
            "location": {
                "name": "Arcimoto World Headquarters",
                "city": "Eugene",
                "state": "Oregon"
            },
            "coverage": "pilot",
            "model": "FUV",
            "telemetry": {
                "odometer": "unknown"
            }
        },
        {
            "vin": "DEV-7F7ATR319MER00028",
            "location": {
                "name": "Arcimoto Rental Facility [San Diego]",
                "city": "San Diego",
                "state": "California"
            },
            "coverage": "rental",
            "model": "FUV",
            "telemetry": {
                "odometer": "unknown"
            }
        },
        {
            "vin": "DEV-7F7ATR319MER00031",
            "location": {
                "name": "Arcimoto Rental Facility [Orlando]",
                "city": "Orlando",
                "state": "Florida"
            },
            "coverage": "rental",
            "model": "FUV",
            "telemetry": {
                "odometer": "unknown"
            }
        },
        {
            "vin": "DEV-7F7ATR319MER00076",
            "location": {
                "name": "Arcimoto Rental Facility [Eugene]",
                "city": "Eugene",
                "state": "Oregon"
            },
            "coverage": "rental",
            "model": "FUV",
            "telemetry": {
                "odometer": {
                    "start": {
                        "point": 735.5852035099999,
                        "time": "2021-08-30T14:18:00Z"
                    },
                    "end": {
                        "point": 735.5852035099999,
                        "time": "2021-08-30T14:18:00Z"
                    }
                }
            }
        },
        {
            "vin": "DEV-7F7ATR31XKER00004",
            "location": {
                "name": "Arcimoto World Headquarters",
                "city": "Eugene",
                "state": "Oregon"
            },
            "coverage": "internal",
            "model": "FUV",
            "telemetry": {
                "odometer": "unknown"
            }
        },
        {
            "vin": "DEV-7F7ATR31XLER00084",
            "location": {
                "name": "Arcimoto World Headquarters",
                "city": "Eugene",
                "state": "Oregon"
            },
            "coverage": "internal",
            "model": "FUV",
            "telemetry": {
                "odometer": {
                    "start": {
                        "point": 3257.77358848,
                        "time": "2021-08-26T22:55:00Z"
                    },
                    "end": {
                        "point": 3257.77358848,
                        "time": "2021-08-31T23:59:00Z"
                    }
                }
            }
        },
        {
            "vin": "DEV-7F7ATR31XLER00117",
            "location": {
                "name": "Arcimoto World Headquarters",
                "city": "Eugene",
                "state": "Oregon"
            },
            "coverage": "internal",
            "model": "FUV",
            "telemetry": {
                "odometer": "unknown"
            }
        },
        {
            "vin": "DEV-7F7ATR31XMER00071",
            "location": {
                "name": "Arcimoto World Headquarters",
                "city": "Eugene",
                "state": "Oregon"
            },
            "coverage": "pilot",
            "model": "FUV",
            "telemetry": {
                "odometer": "unknown"
            }
        },
        {
            "vin": "DEV-7F7ATR31XMER00085",
            "location": {
                "name": "Arcimoto Rental Facility [Eugene]",
                "city": "Eugene",
                "state": "Oregon"
            },
            "coverage": "rental",
            "model": "FUV",
            "telemetry": {
                "odometer": {
                    "start": {
                        "point": 1805.40586792,
                        "time": "2021-08-22T16:26:00Z"
                    },
                    "end": {
                        "point": 2048.0450297100006,
                        "time": "2021-08-31T23:05:00Z"
                    }
                }
            }
        },
        {
            "vin": "DEV-7F7ATR31XMER00099",
            "location": {
                "name": "Arcimoto Rental Facility [Orlando]",
                "city": "Orlando",
                "state": "Florida"
            },
            "coverage": "rental",
            "model": "FUV",
            "telemetry": {
                "odometer": "unknown"
            }
        },
        {
            "vin": "DEV-7F7ATR31XMER00135",
            "location": {
                "name": "Arcimoto Rental Facility [Eugene]",
                "city": "Eugene",
                "state": "Oregon"
            },
            "coverage": "rental",
            "model": "FUV",
            "telemetry": {
                "odometer": {
                    "start": {
                        "point": 5.59855271,
                        "time": "2021-08-30T15:50:00Z"
                    },
                    "end": {
                        "point": 7.3321778,
                        "time": "2021-08-30T22:30:00Z"
                    }
                }
            }
        }
    ]
    }
    args = {
        'json_data': json_data
    }

    def test_yrisk_notify_success(self):
        self.assertIsInstance(yrisk_functions.notify(self.args), dict)

    # test errors
    def test_yrisk_notify_error_input_null_json_data(self):
        args = copy.deepcopy(self.args)
        args['json_data'] = None
        with self.assertRaises(ArcimotoArgumentError):
            yrisk_functions.notify(args)

    def test_yrisk_notify_error_input_empty_json_data(self):
        args = copy.deepcopy(self.args)
        args['json_data'] = []
        with self.assertRaises(ArcimotoArgumentError):
            yrisk_functions.notify(args)

    def test_yrisk_notify_error_input_invalid_type_json_data(self):
        args = copy.deepcopy(self.args)
        args['json_data'] = 'not a list'
        with self.assertRaises(ArcimotoArgumentError):
            yrisk_functions.notify(args)


@arcimoto.runtime.handler
def test_yrisk_notify():
    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(YriskNotifyTestCase)
    ))


lambda_handler = test_yrisk_notify
