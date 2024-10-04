# CAFL: Constraint-guided AFL

CAFL is a fuzzer implementation of "Constraint-guided Directed Greybox Fuzzing"
[USENIX'21]. 

## Installation

 1. Run `install.sh`. This will install `go` and `llvm-8`, and build CAFL.
```
$ ./install.sh
```
 2. Source `SOURCE_ME`. You may either source it before whenever using CAFL or register it in your `.bashrc` if you prefer.
``` 
$ . SOURCE_ME
```

## Overview

|          |afl             |CAFL            |
|----------|----------------|----------------|
|Compiler  |afl-clang-fast  |vsa-clang-fast  |
|          |afl-clang-fast++|vsa-clang-fast++|
|Fuzzer    |afl-fuzz        |vsa-fuzz        |
|Description Path|          |VSA_DESC        |

The overall usage is similar to AFL; some differences include:
  * You need to compile your source code with `vsa-clang-{fast/fast++}`.
  * You need to provide a _constraint description_ at compile time.

## Usage

 1. Write a _constraint description_. Refer to the template descriptions in
    `afl/scripts/templates` for basic format and grammar.

 2. Compile a CAFL-instrumented binary with `vsa-clang-{fast,fast++}`. Your
    description's path should be defined as the `VSA_DESC` environment variable.

  - Using `vsa-clang-fast` directly.
```  
$ VSA_DESC=<your_description_path> vsa-clang-fast <...>
```  
  - Using `vsa-clang-fast` through build script generator tools (e.g.,
    `configure`). Notice that the description must be provided when it actually
    builds something.
```
$ CC=vsa-clang-fast ./configure
$ VSA_DESC=<your_description_path> make
```

 3. Fuzz with `vsa-fuzz`, the CAFL's counterpart of `afl-fuzz`. No additional
    argument is required other than what you need to run `afl-fuzz`.

## Batch Fuzzing 

CAFL supports batch (i.e., parallel) fuzzing in a similar manner to AFL.
`vsa-batch-fuzz` works with the same command line arguments to `vsa-fuzz`,
except it additinally accepts the number of parallel instances `-N` (default:
10). 
 
## Constraint Generator

`afl/scripts` implmements a constraint generator given an ASAN or MSAN crash 
dump. The script extracts necessary information from it and fills out the
placeholders in a corresponding template. The templates can be found in
`afl/scripts/templates`.

(Note: the raw output may be incomplete or inaccurate. You may want to review
and correct it before plugging it into the compiler.)
