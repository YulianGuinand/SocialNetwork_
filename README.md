# SocialNetwork_
# Guide d'installation et de configuration de la base de données

Ce guide vous expliquera comment installer MySQL, importer la base de données et lancer le serveur Django.

## Installation de MySQL

1. Assurez-vous d'avoir accès à un système compatible avec MySQL (Linux, Windows, MacOS).
2. Pour installer MySQL sur votre système, suivez les instructions fournies sur le site officiel de MySQL : [https://dev.mysql.com/doc/mysql-installation-excerpt/8.0/en/](https://dev.mysql.com/doc/mysql-installation-excerpt/8.0/en/)
3. Après avoir installé MySQL, assurez-vous qu'il est en cours d'exécution et notez le nom d'utilisateur et le mot de passe que vous avez utilisés lors de l'installation.

## Importation de la base de données

1. Téléchargez le fichier SQL exporté depuis le projet ( backup.sql ).
2. Ouvrez un terminal ou une ligne de commande.
3. Utilisez la commande suivante pour importer la base de données dans MySQL :

   ```
   mysql -u debian-sys-maint -p db < backup.sql
   ```
Puis vous devrez rentrer ce mot de passe : qbac2COeqQ7o7nXd

## Lancement du serveur Django

1. Assurez-vous d'avoir Python installé sur votre système. Si ce n'est pas le cas, vous pouvez le télécharger à partir du site officiel de Python : [https://www.python.org/downloads/](https://www.python.org/downloads/)
2. Clonez le projet depuis le référentiel GitHub.
3. Accédez au répertoire du projet dans un terminal ou une ligne de commande.
4. Exécutez les migrations Django pour créer les tables nécessaires dans la base de données :

   ```
   python manage.py migrate
   ```

5. Lancez le serveur Django en utilisant la commande suivante :

   ```
   python manage.py runserver
   ```

6. Le serveur Django devrait démarrer et être accessible à l'adresse indiquée dans la console.
