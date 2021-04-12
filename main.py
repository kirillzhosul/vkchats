# Launcher for VK Peer Scaner.

if __name__ == "__main__":
    try:
        import scaner
    except ImportError:
        print("Error when importing core.")
