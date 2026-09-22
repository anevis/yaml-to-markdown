{
  description = "Convert YAML/JSON to Markdown";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs =
    {
      self,
      nixpkgs,
      flake-utils,
    }:
    flake-utils.lib.eachDefaultSystem (
      system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        python3Packages = pkgs.python3Packages;

        version =
          let
            content = builtins.readFile ./src/version.py;
            # build.sh rewrites version.py with single quotes; committed source uses double
            double = builtins.match ".*__version__ = \"([^\"]+)\".*" content;
            single = builtins.match ".*__version__ = '([^']+)'.*" content;
            match = if double != null then double else single;
          in
          builtins.elemAt match 0;

        yaml-to-markdown = python3Packages.buildPythonApplication {
          pname = "yaml-to-markdown";
          inherit version;
          pyproject = true;

          src = pkgs.lib.fileset.toSource {
            root = ./.;
            fileset = pkgs.lib.fileset.unions [
              ./pyproject.toml
              ./README.md
              ./LICENSE
              ./src
            ];
          };

          build-system = with python3Packages; [ hatchling ];

          # pyproject pins an exact hatchling version (bumped by dependabot);
          # nixpkgs ships a nearby version, so drop the pin. Match any version so
          # the build survives future bumps without editing this file.
          postPatch = ''
            sed -i -E "s/hatchling==[0-9]+(\.[0-9]+)*/hatchling/" pyproject.toml
          '';

          dependencies = with python3Packages; [
            click
            pyyaml
            jsonschema
            # jsonschema[format] extras
            fqdn
            idna
            isoduration
            jsonpointer
            rfc3339-validator
            rfc3986-validator
            rfc3987-syntax
            uri-template
            webcolors
          ];

          nativeCheckInputs = with python3Packages; [ pytest ];

          checkPhase = ''
            runHook preCheck
            pytest
            runHook postCheck
          '';

          meta = {
            description = "A library to convert YAML files to Markdown format";
            homepage = "https://github.com/anevis/yaml-to-markdown";
            license = pkgs.lib.licenses.mit;
            mainProgram = "yaml-to-markdown";
            platforms = pkgs.lib.platforms.all;
          };
        };
      in
      {
        packages.default = yaml-to-markdown;
        packages.yaml-to-markdown = yaml-to-markdown;
        checks.default = yaml-to-markdown;
      }
    );
}
