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
  ];
  languages.python = {
    enable = true;
    venv = {
      enable = true;
    };
  };
}
