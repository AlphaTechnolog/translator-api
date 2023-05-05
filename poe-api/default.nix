{ fetchFromGitHub, pkgs, lib, ... }:

with pkgs.python3Packages; buildPythonPackage rec {
  pname = "poe-api";
  version = "0.3.1-py3-none-any";
  doCheck = false;
  patches = [./requirements.diff];
  pythonImportsCheck = ["poe"];
  propagatedBuildInputs = [
    python-socks
    requests
    websocket-client
  ];
  src = fetchFromGitHub {
    owner = "adding2210";
    repo = "poe-api";
    rev = "eaf81df8cf8130ce6a8848465b600dc437e4f222";
    sha256 = "j406gJXWGVolaptDFV/mXj7nWVjtGTnBUz6q66BIjfQ=";
  };
}