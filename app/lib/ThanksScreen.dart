import 'package:app/DonationScreen.dart';
import 'package:flutter/material.dart';
import 'const.dart';

class ThanksPage extends StatefulWidget {
  @override
  State<StatefulWidget> createState() => new _State();
}

class _State extends State<ThanksPage> {
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
                          image: AssetImage('assets/img/ThankYou.png')))),
              // calendar page
              Positioned(
                  bottom: 90.0,
                  left: 125.0,
                  right: 125.0,
                  top: 575.0,
                  child: TextButton(
                    onPressed: () {
                      Navigator.push(
                        context,
                        PageRouteBuilder(
                          pageBuilder: (context, animation1, animation2) =>
                              DonationPage(),
                          transitionDuration: Duration(seconds: 0),
                        ),
                      );
                    },
                    child: Text('', style: TextStyle(fontSize: 15.0)),
                  )),
            ])));
  }
}
