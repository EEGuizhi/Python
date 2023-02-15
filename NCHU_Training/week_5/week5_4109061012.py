# 4109061012 陳柏翔

import torch
import matplotlib.pyplot as plt

if __name__ == "__main__":
    
    # 裝置
    DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

    # Target
    A = 2.0
    B = 3.0
    C = 2.0
    x = torch.linspace(-5, 5, 1000, device=DEVICE, dtype=torch.float)  # 從-5 ~ +5切割1000個點
    target_y = A * x**2 + B * x + C
    target_label = "Target : A = "+str(A)+",  B = "+str(B)+",  C ="+str(C)


    # Predict
    Ada = 1
    square_sumA = 0
    square_sumB = 0
    square_sumC = 0
    para_A = torch.randn((), requires_grad=True, device=DEVICE, dtype=torch.float)
    para_B = torch.randn((), requires_grad=True, device=DEVICE, dtype=torch.float)
    para_C = torch.randn((), requires_grad=True, device=DEVICE, dtype=torch.float)

    for i in range(101):
        MSEloss = (0.5 * (para_A * x**2 + para_B * x + para_C - target_y)**2).sum()

        MSEloss.backward()

        with torch.no_grad():
            square_sumA += para_A.grad**2
            square_sumB += para_B.grad**2
            square_sumC += para_C.grad**2
            para_A -= Ada / (square_sumA)**0.5 * para_A.grad
            para_B -= Ada / (square_sumB)**0.5 * para_B.grad
            para_C -= Ada / (square_sumB)**0.5 * para_C.grad

            para_A.grad = None
            para_B.grad = None
            para_C.grad = None

        pred_y = para_A * x**2 + para_B * x + para_C
        Pred_label = "Predict : A = "+str(round(float(para_A), 2))+",  B ="+str(round(float(para_B), 2))+",  C ="+str(round(float(para_C), 2))
        
        # Plot
        if i == 1:
            plt.subplot(1, 3, 1)
            plt.title("Regression 1")
            plt.plot(x.cpu(), target_y.cpu(), color="red", label=target_label)
            plt.plot(x.cpu().detach().numpy(), pred_y.cpu().detach().numpy(), label=Pred_label)
            plt.legend(loc="upper left")
        elif i == 5:
            plt.subplot(1, 3, 2)
            plt.title("Regression 2")
            plt.plot(x.cpu(), target_y.cpu(), color="red", label=target_label)
            plt.plot(x.cpu().detach().numpy(), pred_y.cpu().detach().numpy(), label=Pred_label)
            plt.legend(loc="upper left")
        elif i == 100:
            plt.subplot(1, 3, 3)
            plt.title("Regression 3")
            plt.plot(x.cpu(), target_y.cpu(), color="red", label=target_label)
            plt.plot(x.cpu().detach().numpy(), pred_y.cpu().detach().numpy(), label=Pred_label)
            plt.legend(loc="upper left")

    # Show
    plt.show()
