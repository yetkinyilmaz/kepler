

class Orbit {



};


class Planet : public Orbit{
public:
  Planet(){
    position.SetXYZ(50,0,0);
    momentum.SetXYZ(0.02,0.05,0);

  }

public:
  TVector3 position;
  TVector3 momentum;

};


void generate(){


  TCanvas* c = new TCanvas("c","c",600,600);
  TH2D* h = new TH2D("h","",500,-100,100,500,-100,100);

  int N = 10000;

  Planet p;

  double g = 0.5;

  //  g = 50;
  //  p.momentum *= 10;

  int key;

  //  while(key != 0){
  for(int i = 0; i < N; ++i){

    TVector3 acceleration = p.position;
    acceleration *= -g * pow(p.position.Mag(),-3);

    p.momentum += acceleration;
    p.position += p.momentum;

    h->Fill(p.position.X(),p.position.Y());
    //    h->Draw("colz");
    //    c->Update();
    if(i % 100 == 0) cout<<i<<" position: "<<p.position.x()<<" , "<<p.position.Y()<<endl; 
    // std::cin>>key;

  }

  h->Draw("colz");

}


