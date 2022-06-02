# drmkms-python-tests
DRM/KMS manual validation scripts

## Motivation
Android UI performance relies on DRM/KMS quality a lot.

Mainline kernel drivers still have bugs that make FULL DRM/KMS support impossible
and we have to limit or disable using HW overlay planes for such drivers/boards.

In addition to that some of the kernel DRM drivers do not expose full hardware capabilities.
Improving such drivers is much faster when easy-to-run test procedures are available.

Also it is nice to have the ability to test any change in driver code for regression with existing tests.

## Running
Scripts depends on kmsxx library: https://github.com/tomba/kmsxx

## Contributing
Contributions are welcome.

Feel free to add any new / fix existing tests by opening a pull request.
