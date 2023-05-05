{
  inputs = {
    nixpkgs.url = github:nixos/nixpkgs;
    flake-utils.url = github:numtide/flake-utils;
  };

  outputs = {self, nixpkgs, flake-utils}: flake-utils.lib.eachDefaultSystem(system: let
    pkgs = nixpkgs.legacyPackages.${system};
    poe-api = pkgs.callPackage ./poe-api {};
    python3 = pkgs.python3.withPackages(ps: with ps; [
      flask
      poe-api
      python-dotenv
    ]);
  in {
    devShells.default = pkgs.mkShell {
      name = "dev-env";
      buildInputs = [python3];
    };
  });
}