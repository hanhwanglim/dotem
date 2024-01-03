# dotem

dotem is a simple Python package designed to streamline the process of loading environment variables into your shell from a `.env.toml` file. It aims to make the configuration of your development environment easier and more consistent.

## Motivation

Managing environment variables is a common task in software development, and it can become cumbersome, especially when dealing with multiple configurations for different environments.

An example of a project with many different `.env` files:

```text
project/
|-- env/
|   |-- .env
|   |-- .env.local
|   |-- .env.development
|   |-- .env.staging
|   |-- .env.uat
|   |-- .env.prod
|   `-- ...
`-- ...
```

dotem was created with the following motivations:

- Simplicity: Provide a straightforward solution for loading environment variables, reducing the complexity of managing configurations using a single file `.env.toml`.
- Consistency: Establish a consistent approach to handling environment variables across projects, using a standardized .env.toml file format.
- Ease of Use: Make it easy for developers to set up their development environment by simply creating a configuration file and loading variables with a single function call.

## Installation

> [!WARNING]  
> `dotem` is supported in Linux and Darwin machines only!

You can install `dotem` using pip. Run the following command:

```bash
pip install dotem
```

Then, in your `.bashrc` or `.zshrc` file, add the following line:

```bash
eval "$("dotem-cli" hook)"
```

## Features

- Loading and unloading environment variables from a `.env.toml` file.
- Simple and lightweight.
- Support TOML format for easy configuration.
- Loading and unloading environment variables with inheritance.

## Usage

1. Create a `.env.toml` file with your environment variables.

    ```toml
    [development]
    API_KEY = "..."
    DATABASE_URL = "..."

    [production]
    API_KEY = "..."
    DATABASE_URL = "..."
    ```

2. In your shell, use `dotem load [profile]` to load the environment variable into your shell.

    ```bash
    dotem load development
    ```

    This will load the environment variables of that profile in your shell.

### Commands

- `dotem load [profile]` - Loads the environment variables defined in the profile.
- `dotem unload [profle]` - Unsets the environment variables defined in the profile.
- `dotem edit` - Edits the `.env.toml` file in the `$EDITOR`
- `dotem hook` - A script to hook up `dotem`
- `dotem --help` - Help
- `dotem [COMMAND] --help` - Command help

## Configuration

### `.env.toml` search path

By default, `dotem` will look for the `.env.toml` file in the current working directory. If there are no `.env.toml` in the current working directory, it will check in the following order:

1. Current working directory (`./env.toml`).
2. Parent directory (`../.env.toml`)
3. `$XDG_CONFIG_HOME/.config/dotem/.env.toml` or `$HOME/.config/dotem/.env.toml` if `$XDG_CONFIG_HOME` is not defined.
4. `$HOME/.env.toml`

### Default profiles

#### The `[global]` profile

The `global` profile is a profile that always gets loaded whenever you call `dotem load [profile]`.

#### The `[default]` profile

If the profile in `dotem load [profile]` is empty, dotem will load the `default` profile. If a `default` profile is not set, it will raise an error.

### Environment variable inheritance

`dotem` supports environment variable inheritance. Suppose we have the following `.env.toml` file:

```toml
[development]
API_KEY = "..."
DATABASE_URL = "..."

[development.zone-a]
ZONE_A_SECRET_USERNAME = "..."
ZONE_A_SECRET_PASSWORD = "..."

[development.zone-b]
ZONE_B_SECRET_USERNAME = "..."
ZONE_B_SECRET_PASSWORD = "..."
```

Running the command `dotem load development.zone-a` will load the parent's environment variables `development` and the child `zone-a`:

- `API_KEY = "..."`
- `DATABASE_URL = "..."`
- `ZONE_A_SECRET_USERNAME = "..."`
- `ZONE_A_SECRET_PASSWORD = "..."`

> [!NOTE]  
> If two of the same environment variable is set in the parent and child profile, dotem will use the environment variable set in the child's profile instead.

## Contributing

Contributions, issues, and feature requests are welcome! Please feel free to submit a pull request or open an issue.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
