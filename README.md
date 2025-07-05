```bash
echo "deb [trusted=yes] https://raw.githubusercontent.com/autowarefoundation/autoware-deb-packages-old/jammy-humble-main-cuda/ ./" | sudo tee /etc/apt/sources.list.d/autowarefoundation_autoware-deb-packages-old-jammy-humble-main-cuda.list
echo "yaml https://github.com/autowarefoundation/autoware-deb-packages-old/raw/jammy-humble-main-cuda/local.yaml humble" | sudo tee /etc/ros/rosdep/sources.list.d/1-autowarefoundation_autoware-deb-packages-old-jammy-humble-main-cuda.list
```
