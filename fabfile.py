set(
    fab_hosts = ['overloaded.org'],
)

def deploy():
    """Update and restart Watercooler."""
    local('hg push')
    run('cd ~/projects/watercooler; hg pull -u')
    run('~/etc/rc.d/watercooler.sh restart')
