{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = {
    self,
    nixpkgs,
    flake-utils,
  }:
    flake-utils.lib.eachDefaultSystem (
      system: let
        pkgs = import nixpkgs {inherit system;};

        pythonEnv = pkgs.python314.withPackages (ps:
          with ps; [
            django
            django-environ
            psycopg2
            pillow
            daphne
            djangorestframework
            django-redis
            django-extensions
            jupyterlab
            python-lsp-server
          ]);
      in {
        devShells.default = pkgs.mkShell {
          buildInputs = [
            pythonEnv
            pkgs.sqlite
            pkgs.postgresql
            pkgs.ruff
            pkgs.act
            pkgs.docker-buildx
            pkgs.pyrefly # python lsp
            pkgs.basedpyright # python lsp
          ];
        };
      }
    );
}
