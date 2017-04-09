
# PSQLFS: Python SQL / PostgreSQL File System

This library is intended to be used as a filesystem wrapper which runs over a
connection-oriented database. Theoretically all SQL databases which support the
required functions should work, but this library is initially oriented towards
**PostgreSQL databases**, so please don't complain if it doesn't work on other
databases.

This filesystem has the following characteristics:

  * Uses `pyfilesystem` for objective demonstrations
  * <del>Thread-safe and is friendly with heterogeneous requests.</del>
  * <del>Row requirements can be lowered to a certain extent.</del>
  * <del>Low performance cost with a reasonable latency</del>

**Keep in mind that this project is still under heavy development, while
performance, stability and security issues persist, therefore should never be
used in production environments until this note is removed.**
