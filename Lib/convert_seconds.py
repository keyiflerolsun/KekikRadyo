# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

# Convert seconds to mm:ss
def convert_seconds(seconds: int):
    seconds %= 24 * 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return "%02d:%02d" % (minutes, seconds)


# Convert hh:mm:ss to seconds
def time_to_seconds(time):
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(str(time).split(":"))))