{
  pkgs,
  lib,
  config,
  inputs,
  ...
}: {
  packages = with pkgs.python313Packages; [
    inquirerpy
    pandas
    paramiko
  ];
  languages.python = {
    enable = true;
    venv = {
      enable = true;
    };
  };
}
