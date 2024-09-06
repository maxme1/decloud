import calendar
import datetime
import mimetypes
import re
from email.utils import formatdate
from pathlib import Path

from starlette import status
from starlette.requests import Request
from starlette.responses import FileResponse, Response


def serve(request: Request, absolute: Path | str, kind: str) -> Response:
    absolute = Path(absolute)
    stat = absolute.stat()
    if not was_modified_since(request.headers.get('HTTP_IF_MODIFIED_SINCE'), stat.st_mtime, stat.st_size):
        return Response(status_code=status.HTTP_304_NOT_MODIFIED)

    content_type, encoding = mimetypes.guess_type(kind)
    content_type = content_type or 'application/octet-stream'

    headers = {
        'Last-Modified': http_date(stat.st_mtime),
    }
    if encoding:
        headers['Content-Encoding'] = encoding
    return FileResponse(absolute, media_type=content_type, headers=headers)


# these 3 functions were copied from Django

def was_modified_since(header, mtime, size):
    try:
        if header is None:
            raise ValueError
        matches = re.match(r"^([^;]+)(; length=([0-9]+))?$", header, re.IGNORECASE)
        header_mtime = parse_http_date(matches[1])
        header_len = matches[3]
        if header_len and int(header_len) != size:
            raise ValueError
        if int(mtime) > header_mtime:
            raise ValueError
    except (AttributeError, ValueError, OverflowError):
        return True
    return False


def http_date(epoch_seconds=None):
    return formatdate(epoch_seconds, usegmt=True)


MONTHS = 'jan feb mar apr may jun jul aug sep oct nov dec'.split()
__D = r'(?P<day>\d{2})'
__D2 = r'(?P<day>[ \d]\d)'
__M = r'(?P<mon>\w{3})'
__Y = r'(?P<year>\d{4})'
__Y2 = r'(?P<year>\d{2})'
__T = r'(?P<hour>\d{2}):(?P<min>\d{2}):(?P<sec>\d{2})'
RFC1123_DATE = re.compile(r'^\w{3}, %s %s %s %s GMT$' % (__D, __M, __Y, __T))
RFC850_DATE = re.compile(r'^\w{6,9}, %s-%s-%s %s GMT$' % (__D, __M, __Y2, __T))
ASCTIME_DATE = re.compile(r'^\w{3} %s %s %s %s$' % (__M, __D2, __T, __Y))


def parse_http_date(date):
    # email.utils.parsedate() does the job for RFC1123 dates; unfortunately
    # RFC7231 makes it mandatory to support RFC850 dates too. So we roll
    # our own RFC-compliant parsing.
    for regex in RFC1123_DATE, RFC850_DATE, ASCTIME_DATE:
        m = regex.match(date)
        if m is not None:
            break
    else:
        raise ValueError("%r is not in a valid HTTP date format" % date)
    try:
        year = int(m['year'])
        if year < 100:
            current_year = datetime.datetime.utcnow().year
            current_century = current_year - (current_year % 100)
            if year - (current_year % 100) > 50:
                # year that appears to be more than 50 years in the future are
                # interpreted as representing the past.
                year += current_century - 100
            else:
                year += current_century
        month = MONTHS.index(m['mon'].lower()) + 1
        day = int(m['day'])
        hour = int(m['hour'])
        min = int(m['min'])
        sec = int(m['sec'])
        result = datetime.datetime(year, month, day, hour, min, sec)
        return calendar.timegm(result.utctimetuple())
    except Exception as exc:
        raise ValueError("%r is not a valid date" % date) from exc
