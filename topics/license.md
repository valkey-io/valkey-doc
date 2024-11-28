---
title: "License"
description: >
    License and trademark information
---


* Valkey is **open source software** released under the terms of the **three clause BSD license**. Most of the Valkey source code was written by Salvatore Sanfilippo and Pieter Noordhuis. A list of other contributors can be found in the git history.

* Valkey is based on the formerly open source Redis, as it was before the
  license of Redis was changed to one that is not open source.
  Read more about this in the [History of Valkey](history.md).
  Redis is a trademark of Redis Ltd. Whenever we use the name Redis in the
  Valkey documentation, we're trying our best to use it in accordance with the
  [Redis Trademark Guidelines](https://redis.com/legal/trademark-guidelines/).

## Licences:

### Three clause BSD license

Every file in the Valkey distribution, with the exception of third party files
specified in the list below, is provided under the following license:

```
Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice,
  this list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright
  notice, this list of conditions and the following disclaimer in the
  documentation and/or other materials provided with the distribution.

* Neither the name of the copyright holder nor the names of its contributors
  may be used to endorse or promote products derived from this software
  without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE.
```

Files in the Valkey distribution that were originally created for Redis when
Redis was still under the three-clause BSD license contain the following license
(which differs from the above text only in one occurrence of "Redis" in the 3rd
clause):

```
Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice,
  this list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright
  notice, this list of conditions and the following disclaimer in the
  documentation and/or other materials provided with the distribution.

* Neither the name of Redis nor the names of its contributors may be used
  to endorse or promote products derived from this software without
  specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE.
```

### Third-party files and licenses

Valkey uses source code from third parties. All this code contains a BSD or BSD-compatible license. The following is a list of third-party files and information about their copyright.

* Valkey uses the [LHF compression library](http://oldhome.schmorp.de/marc/liblzf.html). LibLZF is copyright Marc Alexander Lehmann and is released under the terms of the **two-clause BSD license**.

* Valkey uses the `sha1.c` file that is copyright by Steve Reid and released under the **public domain**. This file is extremely popular and used among open source and proprietary code.

* When compiled on Linux, Valkey uses the [Jemalloc allocator](https://github.com/jemalloc/jemalloc), which is copyrighted by Jason Evans, Mozilla Foundation, and Facebook, Inc and released under the **two-clause BSD license**.

* Inside Jemalloc, the file `pprof` is copyrighted by Google Inc. and released under the **three-clause BSD license**.

* Inside Jemalloc the files `inttypes.h`, `stdbool.h`, `stdint.h`, `strings.h` under the `msvc_compat` directory are copyright Alexander Chemeris and released under the **three-clause BSD license**.

* The libraries **hiredis** and **linenoise** also included inside the Valkey distribution are copyright Salvatore Sanfilippo and Pieter Noordhuis and released under the terms respectively of the **three-clause BSD license** and **two-clause BSD license**.
