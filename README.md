```bash
echo "deb [trusted=yes] https://github.com/autowarefoundation/autoware-deb-packages/raw/jammy-humble-release/2023.05/ ./" | sudo tee /etc/apt/sources.list.d/autowarefoundation_autoware-deb-packages.list
echo "yaml https://github.com/autowarefoundation/autoware-deb-packages/raw/jammy-humble-release/2023.05/local.yaml humble" | sudo tee /etc/ros/rosdep/sources.list.d/1-autowarefoundation_autoware-deb-packages.list
```
