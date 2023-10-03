{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  # buildInputs is for dependencies you'd need "at run time",
  # were you to to use nix-build not nix-shell and build whatever you were working on
  buildInputs = [
        pkgs.clang
        pkgs.libclang
        pkgs.cmake
        pkgs.cargo
        pkgs.rustc
        pkgs.gettext
        pkgs.ncurses
        pkgs.libiconv
        pkgs.pcre2
        pkgs.coreutils
        pkgs.gnugrep
        pkgs.gnused
        pkgs.groff
  ];
  LIBCLANG_PATH = "${pkgs.libclang.lib}/lib";
}
