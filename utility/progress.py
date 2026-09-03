
def progress(current, total, prefix="Progress", width=30):
    percent = current / total
    filled = int(width * percent)
    bar = "█" * filled + "░" * (width - filled)
    print(f"\r{prefix}: [{bar}] {percent:6.2%}",
          end="",
          flush=True)