import 'package:flutter/material.dart';
import 'const.dart';

class DonationPage extends StatefulWidget {
  @override
  State<StatefulWidget> createState() => new _State();
}

class _State extends State<DonationPage> {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
        home: Scaffold(
            appBar: PreferredSize(
                preferredSize: Size.fromHeight(10.0),
                child: AppBar(
                  backgroundColor: HexColor("000000"),
                )),
            body: Stack(children: [
              Container(
                  width: MediaQuery.of(context).size.width,
                  decoration: BoxDecoration(
                      image: DecorationImage(
                          fit: BoxFit.fill,
                          image: AssetImage('assets/img/DonationList.png')))),
              // calendar page
              Positioned(
                  bottom: 525.0,
                  left: 10.0,
                  right: 10.0,
                  top: 90.0,
                  child: TextButton(
                    onPressed: () {
                      // Navigator.push(
                      //     context,
                      //     MaterialPageRoute(
                      //         builder: (context) => CalendarPage()));
                    },
                    child: Text('HERE', style: TextStyle(fontSize: 15.0)),
                  )),
              Positioned(
                  bottom: 375.0,
                  left: 10.0,
                  right: 10.0,
                  top: 250.0,
                  child: TextButton(
                    onPressed: () {
                      // Navigator.push(
                      //     context,
                      //     MaterialPageRoute(
                      //         builder: (context) => CalendarPage()));
                    },
                    child: Text('HERE2', style: TextStyle(fontSize: 15.0)),
                  )),
            ])));
  }
}
