@extends('layouts.master')

@section('title', 'Page Title')

@section('sidebar')
    @parent

    <p>This is appended to the master sidebar.</p>
@endsection

@section('content')
    <p>This is my body content.</p>
    <table>
        <tr><td>Col 1</td><td>Col 2</td></tr>
        @forelse ($events as $event)
            <tr><td>{{ $event->id }} - {{ $event->created_at }} - {{ $event->type }}</td>
            <td>
                @foreach($event->actor as $actorParam)
                    {{$actorParam}}
                @endforeach
            </td>
            </tr>
    @empty
        <p>No users</p>
    @endforelse
    </table>
    {!! $events->render() !!}
@endsection