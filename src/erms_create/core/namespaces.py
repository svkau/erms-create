"""
XML Namespaces for ERMS
"""

ERMS_NAMESPACE = "https://DILCIS.eu/XML/ERMS"
ERMS = "{%s}" % ERMS_NAMESPACE

XSI_NAMESPACE = "http://www.w3.org/2001/XMLSchema-instance"
XSI = "{%s}" % XSI_NAMESPACE

ROOT_NSMAP = {None: ERMS_NAMESPACE, "xsi": XSI_NAMESPACE}
ERMS_NSMAP = {None: ERMS_NAMESPACE}
