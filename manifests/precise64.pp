class tirpan {
  exec { 'apt-get update':
    command => '/usr/bin/apt-get update'
  }

  package { ["python-pip", "python-gtk2", "curl"]:
    ensure => present
  }

  define pip($version = undef, $ensure) {
    case $ensure {
      present: {
        exec { "pip-install-$name-$version":
        command => "/usr/bin/pip install $name",
        timeout => "-1",
        }
      }
    }
  }


}

include tirpan
tirpan::pip { "nose":
  ensure => present
}