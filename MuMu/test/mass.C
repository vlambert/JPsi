double mass(double pt1, double eta1, double phi1, double m1, double pt2, double eta2, double phi2, double m2) {
  TLorentzVector p1, p2;
  p1.SetPtEtaPhiM(pt1, eta1, phi1, m1);
  p2.SetPtEtaPhiM(pt2, eta2, phi2, m2);
  return (p1+p2).M();
}
