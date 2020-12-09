# nome_in_codice

## Useful libraries
- https://discordpy.readthedocs.io/en/latest/quickstart.html

## TO-DO
- Cercare bot simili
- Bot easy per pasticciare
- Fare diagramma delle classi e assegnare il lavoro

## Doc
Per stampare la documentazione andare nella cartella `docs` e dare il comando `make html`

## Docker
To run the program with docker first you have to clone the repository with `git clone https://github.com/rho9/nome_in_codice.git` or `git clone git@github.com:rho9/nome_in_codice.git`, then you can `cd` in the `nome_in_codice` cloned directory.

The docker image is **not** hosted in any registry at the moment (will be added in the near future), so you have to build the image yourself.

1. Let's start by running `docker build -t discord_nome_in_codice .`. This command will use the Dockerfile in the current directory to produce a valid docker image named *discord_nome_in_codice*.

2. Run the container! `docker run --env-file .env discord_nome_in_codice`.

### env file
PS We used an env file to provide the required variables to the program, the env file should include the following variables:
- `DISCORD_TOKEN` the token for the comunication with discord's APIs
- `DISCORD_GUILD` the name you want to give to the bot
- `HOST_DB` the ip/url where your mysql database is reachable
- `PORT_DB` the port of your mysql database
- `USER_DB` the user of your mysql database
- `PASSWORD_DB`the password of your mysql database
- `DATABASE` the databse name
