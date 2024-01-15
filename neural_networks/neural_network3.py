class Inception_module(torch.nn.Module):
    def __init__(self):
        super(Inception_module, self).__init__()
        
        self.conv1 = torch.nn.Conv2d(3,24, kernel_size=7, stride=2, padding=0)
        self.maxpool1 = torch.nn.MaxPool2d(2, stride=2, padding=0)
        self.batchnorm1 = torch.nn.BatchNorm2d(24)
        self.conv2 = torch.nn.Conv2d(24,192, kernel_size=1, stride=1, padding=0)
        self.conv3 = torch.nn.Conv2d(192,192, kernel_size=3, stride=1, padding=0)
        self.batchnorm2 = torch.nn.BatchNorm2d(192)
        self.maxpool2 = torch.nn.MaxPool2d(30, stride=1, padding=0)
        
        self.conv1x1 = torch.nn.Conv2d(192,48, kernel_size=1, stride=1, padding=0)
        self.conv3x3 = torch.nn.Conv2d(192,80, kernel_size=3, stride=1, padding=1)
        self.conv5x5 = torch.nn.Conv2d(192,32, kernel_size=5, stride=1, padding=2)
        self.maxpool3 = torch.nn.MaxPool2d(2, stride=1, padding=1)
        self.dim_red = torch.nn.Conv2d(192,32, kernel_size=2, stride=1, padding=0)
        
        self.conv1x1_2 = torch.nn.Conv2d(192,48, kernel_size=1, stride=1, padding=0)
        self.conv3x3_2 = torch.nn.Conv2d(192,80, kernel_size=3, stride=1, padding=1)
        self.conv5x5_2 = torch.nn.Conv2d(192,32, kernel_size=5, stride=1, padding=2)
        self.maxpool3_2 = torch.nn.MaxPool2d(2, stride=1, padding=1)
        self.dim_red_2 = torch.nn.Conv2d(192,32, kernel_size=2, stride=1, padding=0)


    def forward(self, x):
        x = self.conv1(x)
        x = self.maxpool1(x)
        x = self.batchnorm1(x)
        x = self.conv2(x)
        x = self.conv3(x)
        x = self.batchnorm2(x)
        x = self.maxpool2(x)

        x1 = self.conv1x1(x)
        x3 = self.conv3x3(x)
        x5 = self.conv5x5(x)
        xmaxp = self.maxpool3(x)
        xmaxr = self.dim_red(xmaxp)
        x = torch.cat((x1, x3, x5, xmaxr),1)

        x1 = self.conv1x1_2(x)
        x2 = self.conv3x3_2(x)
        x3 = self.conv5x5_2(x)
        x4 = self.maxpool3_2(x)
        x4 = self.dim_red_2(x4)
        x = torch.cat((x1, x2, x3, x4),1)

        return x