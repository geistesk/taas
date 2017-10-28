with import <nixpkgs> {};

(pkgs.python36.withPackages (ps: [ps.irc])).env
