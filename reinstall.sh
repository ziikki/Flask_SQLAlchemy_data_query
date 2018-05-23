brew remove mysql

brew cleanup

launchctl unload -w ~/Library/LaunchAgents/com.mysql.mysqld.plist

rm ~/Library/LaunchAgents/com.mysql.mysqld.plist

sudo rm -rf /usr/local/var/mysql

brew install mysql

unset TMPDIR

mysql_install_db --verbose --user=`whoami` --basedir="$(brew --prefix mysql)" --datadir=/usr/local/var/mysql --tmpdir=/tmp

mkdir -p ~/Library/LaunchAgents
cp /usr/local/Cellar/mysql/5.5.25a/homebrew.mxcl.mysql.plist ~/Library/LaunchAgents/
launchctl load -w ~/Library/LaunchAgents/homebrew.mxcl.mysql.plist
