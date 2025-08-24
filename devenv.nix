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
    pyinstaller
    nuitka
  ];
  languages.python = {
    enable = true;
    venv = {
      enable = true;
    };
  };
}
