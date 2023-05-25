```bash
echo "deb [trusted=yes] https://raw.githubusercontent.com/autowarefoundation/autoware-deb-packages/some-random-test-branch/ ./" | sudo tee /etc/apt/sources.list.d/autowarefoundation_autoware-deb-packages.list
echo "yaml https://raw.githubusercontent.com/autowarefoundation/autoware-deb-packages/some-random-test-branch/local.yaml humble" | sudo tee /etc/ros/rosdep/sources.list.d/1-autowarefoundation_autoware-deb-packages.list
```
