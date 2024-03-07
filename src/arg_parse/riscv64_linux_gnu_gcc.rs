pub struct Riscv64LinuxGnuGcc<'a> {
    pub input: &'a str,
    pub output: &'a str,
}

pub fn parse<'a, W>(args: W) -> Result<Riscv64LinuxGnuGcc<'a>, ()>
where
    W: Iterator<Item = &'a str>,
{
    let mut iter = args.filter(|&x| !(x.starts_with('-') && x != "-o"));
    let mut input: Option<&'a str> = None;
    let mut output: Option<&'a str> = None;

    while let Some(arg) = iter.next() {
        if arg == "-o" {
            let x = std::mem::replace(&mut output, iter.next());
            if x.is_some() {
                return Err(());
            }
        } else {
            input = Some(arg);
        }
    }
    match (input, output) {
        (Some(input), Some(output)) => Ok(Riscv64LinuxGnuGcc {
            input: input,
            output: output,
        }),
        _ => Err(()),
    }
}

#[cfg(test)]
mod test {
    use super::parse;

    #[test]
    fn smoke_test() {
        /*
        # Compile C source code into RISC-V assembly
        riscv64-linux-gnu-gcc hello.c -S -fsigned-char -o hello.S

        # Link to an RISC-V executable
        riscv64-linux-gnu-gcc -static hello.S -o hello
        */
        assert!(parse(["hello.c", "-S", "-fsigned-char", "-o", "hello.S"].into_iter()).is_ok());
        assert!(parse(["-static", "hello.S", "-o", "hello"].into_iter()).is_ok());
    }
}
