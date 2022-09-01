import os
import torch

root_dir = os.getcwd()


def thin_pth():
    pth_path = 'resnet50.pth'
    state_dict = torch.load(os.path.join(root_dir, pth_path))
    work_dir = os.path.dirname(pth_path)
    pth_name = str(os.path.basename(pth_path)).split('.')[0]
    out_path = os.path.join(root_dir, work_dir, f'{pth_name}_thin.pth')
    torch.save(state_dict['state_dict'], out_path)
    print("Thin pth successful")
    print('| save path:', out_path)


if __name__ == '__main__':
    thin_pth()
