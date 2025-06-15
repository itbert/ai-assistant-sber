# cli.py

import click
import subprocess
import os
from pathlib import Path

@click.group()
def cli():
    """CLI для управления проектом AI For Good"""
    pass


@cli.command()
def run_bot():
    """Запустить Telegram-бота"""
    click.echo("🚀 Запуск Telegram-бота...")
    os.chdir("ai_for_good_bot")
    subprocess.run(["python", "main.py"])


@cli.command()
def run_ai_news_parser():
    """Запустить парсер AI News"""
    click.echo("🕷️ Запуск парсера artificialintelligence-news.com...")
    os.chdir("parsers")
    subprocess.run(["python", "parser_ai_news.py"])


@cli.command()
def run_nature_parser():
    """Запустить парсер Nature.com"""
    click.echo("🕷️ Запуск парсера nature.com...")
    os.chdir("parsers")
    subprocess.run(["python", "parser_nature.py"])


@cli.command()
def run_executor():
    """Запустить обработку данных и загрузку в БД"""
    click.echo("🧠 Запуск Executor'а...")
    os.chdir("executor")
    subprocess.run(["python", "executor.py"])


@cli.command()
def update_all():
    """Обновить все данные: парсеры → обработка → БД"""
    click.echo("🔄 Обновление всех данных...")
    subprocess.run(["python", "cli.py", "parser", "run", "ai-news"])
    subprocess.run(["python", "cli.py", "parser", "run", "nature"])
    subprocess.run(["python", "cli.py", "executor", "run"])


@cli.command()
def build_docker():
    """Собрать Docker-образ"""
    click.echo("🐋 Сборка Docker-образа...")
    subprocess.run(["docker", "build", "-t", "ai-for-good-bot", "."])


@cli.command()
def run_docker():
    """Запустить Docker-контейнер"""
    click.echo("🐋 Запуск Docker-контейнера...")
    subprocess.run([
        "docker", "run",
        "--volume", f"{Path.cwd()}/data:/app/data",
        "--env-file", ".env",
        "ai-for-good-bot"
    ])


if __name__ == "__main__":
    cli()