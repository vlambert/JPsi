{
  Int_t n=20;
  Double_t x[n],y[n],ex[n],ey[n];
  for (Int_t i=0; i < n; i++) {
    x[i]=i*0.1;
    y[i]=10*sin(x[i]+0.2);
    ex[i]=0.05;
    ey[i]=1.;
  }
  TGraphErrors *gr1 = new TGraphErrors(n,x,y,ex,ey);
  TAxis *axis = gr1->GetXaxis();
  axis->SetLimits(-1.,5.); // along X
  gr1->GetHistogram()->SetMaximum(20.); // along
  gr1->GetHistogram()->SetMinimum(-20.); // Y
  gr1->Draw("AC*");
}