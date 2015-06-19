<?php

namespace App\Http\Controllers;

use App\Ghevent;
use App\Http\Controllers\Controller;

class GheventController extends Controller
{
    public function index()
    {
        $events = Ghevent::orderBy('created_at', 'ASC')->simplePaginate(15);

        return view('ghevent.index', ['events' => $events]);
    }

    public function indexJSON()
    {
        $events = Ghevent::take(100)
            ->orderBy('created_at','ASC')
            ->get();

        return response()->json($events);
    }

    public function getActivityType($type)
    {
        $events = Ghevent::take(100)
            ->where('type',$type)
            ->orderBy('created_at','ASC')
            ->get();

       return response()->json($events);
    }

    public function mostPopular()
    {
        $events = DB::select('select * from article where id = ?', array(1));
        return response()->json($events);
    }
}