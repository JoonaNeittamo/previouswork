class Inception_module(torch.nn.Module):
    def __init__(self):
        super(Inception_module, self).__init__()
        
        self.convtop1 = torch.nn.Conv2d(192,80, kernel_size=1, stride=1, padding=0)
        self.convtop2 = torch.nn.Conv2d(192,32, kernel_size=1, stride=1, padding=0)
        self.maxpool1 = torch.nn.MaxPool2d(2, stride=1, padding=1)
        
        self.convbot1 = torch.nn.Conv2d(192,48, kernel_size=1, stride=1, padding=0)
        self.convbot2 = torch.nn.Conv2d(80,80, kernel_size=1, stride=1, padding=0)
        self.convbot3 = torch.nn.Conv2d(32,32, kernel_size=1, stride=1, padding=0)
        self.convbot4 = torch.nn.Conv2d(192,32, kernel_size=2, stride=1, padding=0)
        
        
    def forward(self, x):
        x1 = self.convbot1(x)
        
        x2 = self.convtop1(x)
        x2 = self.convbot2(x2)
        
        x3 = self.convtop2(x)
        x3 = self.convbot3(x3)
        
        x4 = self.maxpool1(x)
        x4 = self.convbot4(x4)
        
        x = torch.cat((x1, x2, x3, x4),1)
        
        return x