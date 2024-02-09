def run(username: str | None = None) -> None:
    username = username or "User"
    print(f"Hello, dear {username}!")


if __name__ == "__main__":
    run()
